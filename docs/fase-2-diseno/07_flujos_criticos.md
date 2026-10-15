# 07 — Flujos críticos (diagramas de secuencia)

| Campo | Valor |
|---|---|
| **Proyecto** | FerreStock — Sistema web de inventario para ferretería |
| **Nombre** | 07_flujos_criticos.md |
| **Descripción** | Diagramas de secuencia en Mermaid de las operaciones críticas: inicio de sesión con "Recordarme", venta concurrente, compra, devolución, ajuste, anulación y reporte de fallos a Taiga. |
| **Fecha de creación** | 2026-10-14 |
| **Fecha de actualización** | 2026-10-14 |
| **Autores** | Ana Sofía Nagles García · María Mercedes Rincón Valencia · Juan David Camacho Tapiero |
| **Versión** | 0.1.0 |
| **Estado** | Aprobado por el equipo (2026-10-14) |

---

## 1. Inicio de sesión y "Recordarme" (CU-01; CA-AUT-01 a 03)

```mermaid
sequenceDiagram
    actor U as Usuario
    participant F as Frontend
    participant S as Spring Security
    participant A as AutenticacionController
    participant DB as PostgreSQL
    F->>S: GET /api/v1/auth/csrf
    S-->>F: 204 + cookie XSRF-TOKEN
    U->>F: usuario, contraseña, [x] Recordarme
    F->>A: POST /auth/login (X-XSRF-TOKEN)
    A->>DB: buscar usuario (activo, bloqueado_hasta)
    alt credenciales válidas
        A->>S: authenticate() + guardar SecurityContext en la sesión
        A->>DB: intentos_fallidos = 0; INSERT auditoria LOGIN_EXITOSO
        opt recordarme = true
            S->>DB: INSERT persistent_logins (serie, token)
            S-->>F: Set-Cookie FSRECUERDAME (7 días)
        end
        A-->>F: 200 SesionResponse + Set-Cookie FSSESSION
    else inválidas
        A->>DB: intentos_fallidos + 1 (bloquear si llega a 5); auditoria LOGIN_FALLIDO
        A-->>F: 401 CREDENCIALES_INVALIDAS (mensaje genérico)
    end
    Note over F,S: Días después: FSSESSION ya expiró, pero FSRECUERDAME sigue vigente
    F->>S: GET /auth/sesion (cookie FSRECUERDAME)
    S->>DB: validar serie y token; rotar el token
    S-->>F: 200 + nueva FSSESSION (sin volver a escribir la contraseña)
```

## 2. Venta con pago en efectivo y concurrencia (CU-06; CA-VEN-01 a 03)

```mermaid
sequenceDiagram
    actor U as Operativo
    participant F as Frontend
    participant VC as VentaController
    participant VS as VentaService
    participant MS as MovimientoInventarioService
    participant CS as ConsecutivoService
    participant DB as PostgreSQL
    U->>F: cliente, líneas, efectivo recibido
    F->>VC: POST /ventas
    VC->>VC: @Valid VentaRequest; @PreAuthorize(ADMIN, OPERATIVO)
    VC->>VS: registrar(request, usuario)
    activate VS
    Note over VS,DB: @Transactional (una sola transacción)
    VS->>DB: cliente activo y es_cliente
    VS->>DB: SELECT productos … ORDER BY id FOR UPDATE
    VS->>VS: validar ACTIVO, fracciones y existencias ≥ cantidad
    alt alguna línea sin existencias
        VS-->>VC: ExistenciasInsuficientesException
        VC-->>F: 409 EXISTENCIAS_INSUFICIENTES (ROLLBACK)
    else todo válido
        VS->>VS: precio vigente → subtotales → total; valorRecibido ≥ total → cambio
        VS->>CS: siguiente("VENTA") [FOR UPDATE en consecutivo]
        VS->>DB: INSERT venta + venta_linea (costo_unitario = CPP vigente)
        loop por cada línea
            VS->>MS: registrarSalida(producto, cantidad, VENTA, ventaId)
            MS->>DB: INSERT movimiento; UPDATE producto.existencias
        end
        VS->>DB: INSERT auditoria VENTA_REGISTRADA
        VS-->>VC: VentaResponse
        VC-->>F: 201 (consecutivo, total, cambio)
    end
    deactivate VS
    Note over VS,DB: Una segunda venta simultánea del mismo producto espera en FOR UPDATE,<br/>luego ve el saldo nuevo y recibe 409 si ya no alcanza. Las existencias nunca quedan negativas.
```

## 3. Compra con varias líneas y CPP (CU-05; CA-COM-01, CA-COS-01)

```mermaid
sequenceDiagram
    participant F as Frontend
    participant CS as CompraService
    participant MS as MovimientoInventarioService
    participant DB as PostgreSQL
    F->>CS: POST /compras {proveedorId, lineas[]}
    Note over CS,DB: @Transactional
    CS->>DB: proveedor activo y es_proveedor
    CS->>CS: sin productos repetidos; cantidad > 0; costo ≥ 0
    CS->>DB: productos ORDER BY id FOR UPDATE (todos ACTIVOS)
    CS->>DB: consecutivo COMPRA; INSERT compra + líneas
    loop línea
        CS->>MS: registrarEntrada(producto, q, c, COMPRA, ponderar = true)
        MS->>MS: Q' = Q + q ; C' = (Q·C + q·c) / Q'
        MS->>DB: INSERT movimiento (C anterior, C'); UPDATE producto
    end
    CS->>DB: auditoria COMPRA_REGISTRADA
    CS-->>F: 201 CompraResponse
```

## 4. Devolución con validación por línea (CU-08; CA-DEV-01 a 03)

```mermaid
sequenceDiagram
    participant F as Frontend
    participant DS as DevolucionService
    participant MS as MovimientoInventarioService
    participant DB as PostgreSQL
    F->>DS: POST /devoluciones {clienteId, ventaId?, motivo, lineas[resultado]}
    Note over DS,DB: @Transactional
    opt con venta
        DS->>DB: venta REGISTRADA del mismo cliente; venta_linea FOR UPDATE
        DS->>DS: devuelta + cantidad ≤ vendida (solo en líneas ACEPTADAS)
    end
    DS->>DB: consecutivo DEVOLUCION; INSERT devolución + líneas
    loop línea ACEPTADA
        alt con venta
            DS->>MS: registrarEntrada(c = costo histórico de la línea, ponderar = true)
            DS->>DB: venta_linea.cantidad_devuelta += cantidad
        else sin venta
            DS->>MS: registrarEntrada(c = CPP vigente, ponderar = false)
        end
    end
    DS->>DB: auditoria DEVOLUCION_REGISTRADA (o DEVOLUCION_SIN_VENTA), validada_por
    DS-->>F: 201
```

## 5. Ajuste autorizado y rechazado (CU-09; CA-AJU-01 a 04)

```mermaid
sequenceDiagram
    actor O as Operativo
    actor A as Administrador
    participant AC as AjusteController
    participant AS as AjusteService
    participant MS as MovimientoInventarioService
    O->>AC: POST /ajustes
    AC-->>O: 403 ACCESO_DENEGADO (@PreAuthorize hasRole ADMIN) + auditoria ACCESO_DENEGADO
    A->>AC: POST /ajustes {SALIDA, 3, motivo}
    AC->>AS: registrar()
    AS->>MS: registrarSalida(producto FOR UPDATE)
    alt existencias < 3
        MS-->>AC: 409 EXISTENCIAS_INSUFICIENTES (sin cambios)
    else
        MS-->>AS: movimiento AJUSTE_SALIDA
        AS-->>AC: 201 + auditoria AJUSTE_REGISTRADO
    end
```

## 6. Anulación de una venta (RF-VEN-006 [P])

```mermaid
sequenceDiagram
    actor A as Administrador
    participant VS as VentaService
    participant MS as MovimientoInventarioService
    participant DB as PostgreSQL
    A->>VS: POST /ventas/{id}/anulacion {motivo}
    VS->>DB: venta FOR UPDATE
    alt estado ≠ REGISTRADA o alguna línea con cantidad_devuelta > 0
        VS-->>A: 409 VENTA_CON_DEVOLUCIONES / ESTADO_INVALIDO
    else
        loop línea
            VS->>MS: registrarEntrada(ANULACION_VENTA, costo histórico, ponderar = true)
        end
        VS->>DB: estado = ANULADA, motivo, anulada_por, anulada_en
        VS->>DB: auditoria VENTA_ANULADA
        VS-->>A: 200
    end
```

## 7. Pipeline: desplegar o reportar a Taiga (CU-13; CA-MON-01, 02)

```mermaid
sequenceDiagram
    actor D as Integrante
    participant G as GitHub
    participant CI as GitHub Actions
    participant T as Taiga API
    participant P as Plataforma de despliegue
    D->>G: git push (develop / main)
    G->>CI: evento push
    CI->>CI: compilar → unitarias → integración (PostgreSQL) → mutación* → build → E2E*
    alt todo en verde y rama main
        CI->>P: desplegar
        CI->>P: GET /actuator/health = UP
        CI->>T: si existe un issue "CI" abierto para este job → comentar "resuelto" y cerrar
    else algún paso falla
        CI->>T: POST /api/v1/auth → token
        CI->>T: GET /issues?project&tags=ci,<repo>,<job>&status__is_closed=false
        alt ya existe
            CI->>T: PATCH issue (comentario con commit, autor y enlace al log)
        else no existe
            CI->>T: POST /issues (asunto, descripción, tags, prioridad, asignado = autor mapeado)
        end
        T-->>D: notificación por correo (asignado + observadores del proyecto)
        CI-->>G: estado fallido (no se despliega)
    end
```

\* La mutación (PIT) y el E2E completo se ejecutan en `main` y en los pull requests hacia `main`, para ahorrar minutos gratuitos (ver 08_repositorios_y_entrega.md).
