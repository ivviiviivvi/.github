/**
 * OpenTelemetry Setup Example
 *
 * This file demonstrates how to set up OpenTelemetry for comprehensive observability.
 * Copy this to your src/instrumentation.js and customize as needed.
 */

const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { OTLPMetricExporter } = require('@opentelemetry/exporter-metrics-otlp-http');
const { PeriodicExportingMetricReader } = require('@opentelemetry/sdk-metrics');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

// Configure resource with service information
const resource = new Resource({
  [SemanticResourceAttributes.SERVICE_NAME]: process.env.SERVICE_NAME || 'my-service',
  [SemanticResourceAttributes.SERVICE_VERSION]: process.env.SERVICE_VERSION || '1.0.0',
  [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV || 'development',
});

// Configure trace exporter
const traceExporter = new OTLPTraceExporter({
  url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318/v1/traces',
  headers: {
    'api-key': process.env.OTEL_API_KEY,
  },
});

// Configure metrics exporter
const metricReader = new PeriodicExportingMetricReader({
  exporter: new OTLPMetricExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318/v1/metrics',
    headers: {
      'api-key': process.env.OTEL_API_KEY,
    },
  }),
  exportIntervalMillis: 60000, // Export every 60 seconds
});

// Initialize SDK
const sdk = new NodeSDK({
  resource,
  traceExporter,
  metricReader,
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-http': {
        requestHook: (span, request) => {
          span.setAttribute('http.user_agent', request.headers['user-agent']);
        },
      },
      '@opentelemetry/instrumentation-express': {
        requestHook: (span, info) => {
          span.setAttribute('express.route', info.route);
        },
      },
    }),
  ],
});

// Start SDK
sdk.start();

// Graceful shutdown
process.on('SIGTERM', () => {
  sdk
    .shutdown()
    .then(() => console.log('Tracing terminated'))
    .catch((error) => console.log('Error terminating tracing', error))
    .finally(() => process.exit(0));
});

// Export for manual instrumentation
const { trace, metrics } = require('@opentelemetry/api');

module.exports = {
  tracer: trace.getTracer(process.env.SERVICE_NAME || 'my-service'),
  meter: metrics.getMeter(process.env.SERVICE_NAME || 'my-service'),
};

/**
 * USAGE EXAMPLES:
 *
 * 1. Require at app start:
 *    require('./instrumentation');
 *
 * 2. Manual tracing:
 *    const { tracer } = require('./instrumentation');
 *    const span = tracer.startSpan('my-operation');
 *    // do work
 *    span.end();
 *
 * 3. Custom metrics:
 *    const { meter } = require('./instrumentation');
 *    const counter = meter.createCounter('my_counter');
 *    counter.add(1, { label: 'value' });
 *
 * 4. Environment variables:
 *    OTEL_EXPORTER_OTLP_ENDPOINT=https://otlp.example.com
 *    OTEL_API_KEY=your-api-key
 *    SERVICE_NAME=my-app
 *    SERVICE_VERSION=1.2.3
 */
