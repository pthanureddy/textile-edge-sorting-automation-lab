# Unified Namespace And OT Integration Contract

## Purpose

The lab publishes each sorting decision under a deterministic Unified Namespace (UNS) path. The hierarchy separates asset identity from the information type so other manufacturing applications can subscribe without depending on the edge service's internal module structure.

## Topic Hierarchy

```text
enterprise/site/area/line/cell/asset/information-type/event
```

For the included station, a classification state message uses:

```text
portfolio/lab/textile-sorting/line-1/edge-cell/sorter-01/state/classification
```

`UnsAddress` validates every hierarchy segment, rejects MQTT wildcards in publisher-owned addresses, and keeps topic construction in one module. The message body includes station identity, route, confidence, reason, actuator command, and UTC timestamp.

## OT Boundary

The same decision is represented in three integration contracts:

- MQTT/UNS for event distribution to production-near IT services.
- OPC UA node identifiers for a PLC or gateway-facing namespace mapping.
- InfluxDB line protocol for time-series storage and operational analysis.

These are deterministic software contracts. The repository does not claim a live MQTT broker, PLC, OPC UA server, industrial network, or production deployment.

## Production Extension Path

A production implementation would add broker authentication and TLS, QoS and retained-message policy, schema versioning, birth/death or availability messages, store-and-forward handling, OPC UA client/server connectivity, observability, and tests against the customer's actual OT network and equipment.
