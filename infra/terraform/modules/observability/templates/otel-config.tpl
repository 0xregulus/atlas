receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318
processors:
  batch: {}
exporters:
  logging: {}
%{ if prometheus_remote_write != "" }
  prometheusremotewrite:
    endpoint: "${prometheus_remote_write}"
%{ endif }
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging%{ if prometheus_remote_write != "" }, prometheusremotewrite%{ endif }]
