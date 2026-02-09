# Monitoring Stack Setup

This project includes a complete monitoring stack using Prometheus and Grafana to track the health of backend and frontend services.

## Components

- **Prometheus**: Collects and stores metrics as time series data
- **Grafana**: Visualizes the metrics collected by Prometheus
- **Service Monitors**: Configures Prometheus to automatically discover and monitor services

## Prerequisites

- Kubernetes cluster with kubectl configured
- Helm (optional, for easier deployment)

## Installation

### Option 1: Using kubectl (Manual Installation)

1. Apply the monitoring namespace:
   ```bash
   kubectl apply -f monitoring/namespace.yaml
   ```

2. Apply the Prometheus configuration:
   ```bash
   kubectl apply -f monitoring/prometheus-config.yaml
   ```

3. Apply the Prometheus deployment:
   ```bash
   kubectl apply -f monitoring/prometheus-deployment.yaml
   ```

4. Apply the Grafana configuration:
   ```bash
   kubectl apply -f monitoring/grafana-deployment.yaml
   ```

5. Apply the service monitors:
   ```bash
   kubectl apply -f monitoring/service-monitors.yaml
   ```

### Option 2: Using Helm (Recommended)

If you prefer to use Helm charts for easier management:

1. Add the Prometheus community Helm repository:
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo add grafana https://grafana.github.io/helm-charts
   helm repo update
   ```

2. Install Prometheus and Grafana:
   ```bash
   helm install prometheus prometheus-community/kube-prometheus-stack \
     --namespace monitoring \
     --create-namespace \
     --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
     --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false
   ```

## Accessing the Services

### Prometheus
After installation, access Prometheus at:
```bash
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090
```
Then navigate to `http://localhost:9090`

### Grafana
Access Grafana at:
```bash
kubectl port-forward -n monitoring svc/grafana-service 3000:3000
```
Then navigate to `http://localhost:3000`

Default credentials:
- Username: `admin`
- Password: `admin123` (change this in production!)

## Monitoring Configuration

The monitoring stack is configured to:

1. Scrape metrics from Kubernetes components (API servers, nodes, pods)
2. Monitor the todo-backend service on port 8001
3. Monitor the todo-frontend service on port 3000
4. Collect standard system metrics (CPU, memory, disk, network)

## Dashboard Import

To import the preconfigured dashboard:

1. Access Grafana at `http://localhost:3000`
2. Click on the gear icon (⚙️) in the left sidebar
3. Select "Dashboards"
4. Click "New" and then "Import"
5. Copy the content from `monitoring/dashboard-config.json` and paste it into the textbox
6. Click "Load" and then "Import"

## Metrics Collection

The system collects various metrics including:

### Backend Service Metrics
- Service availability (`up` metric)
- HTTP request rates
- Response times
- Error rates
- Resource utilization (CPU, memory)

### Frontend Service Metrics
- Service availability (`up` metric)
- HTTP request rates
- Response times
- Error rates
- Resource utilization (CPU, memory)

### System Metrics
- Node resource utilization
- Pod resource utilization
- Kubernetes component health

## Alerting

Prometheus can be configured with alerting rules. To add alerts:

1. Create a rules file with your alerting rules
2. Mount it to the Prometheus pod
3. Reload Prometheus configuration

Example alerting rule:
```yaml
groups:
- name: todo-app-alerts
  rules:
  - alert: BackendDown
    expr: up{job="todo-backend"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Backend service is down"
      description: "The backend service has been down for more than 1 minute"
```

## Troubleshooting

### Check Prometheus Status
```bash
kubectl get pods -n monitoring | grep prometheus
kubectl logs -n monitoring deployment/prometheus-deployment
```

### Check Grafana Status
```bash
kubectl get pods -n monitoring | grep grafana
kubectl logs -n monitoring deployment/grafana-deployment
```

### Verify Service Discovery
1. Access Prometheus web UI
2. Go to "Status" → "Targets"
3. Verify that your services appear as targets and are being scraped

### Common Issues
- If services aren't being discovered, ensure they have the correct labels and annotations
- If metrics aren't showing up, check Prometheus logs for configuration errors
- If Grafana can't connect to Prometheus, verify the datasource configuration

## Production Considerations

For production environments, consider:

- Securing Grafana with strong passwords and authentication
- Setting up persistent storage for Prometheus and Grafana
- Configuring alerting with notification channels (Slack, email, etc.)
- Implementing proper backup strategies
- Setting up resource limits and requests appropriately
- Using TLS for all communications
- Regular security updates