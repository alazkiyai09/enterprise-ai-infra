"""
Data ingestion layer for consuming and producing messages.
"""

from src.pipeline.ingestion.consumer import (
    MessageConsumer,
    RedisConsumer,
    KafkaConsumer,
    get_redis_client,
    get_async_redis_client,
)
from src.pipeline.ingestion.producer import (
    MessageProducer,
    RedisProducer,
    KafkaProducer,
)
from src.pipeline.ingestion.ingest_service import (
    IngestService,
    AdEvent,
    EventType,
    BatchStatus,
    BatchIngestRequest,
    BatchIngestResponse,
    SingleIngestRequest,
    SingleIngestResponse,
    BatchStatusResponse,
    router as ingest_router,
)

__all__ = [
    # Consumers
    "MessageConsumer",
    "RedisConsumer",
    "KafkaConsumer",
    "get_redis_client",
    "get_async_redis_client",
    # Producers
    "MessageProducer",
    "RedisProducer",
    "KafkaProducer",
    # Ingestion Service
    "IngestService",
    "AdEvent",
    "EventType",
    "BatchStatus",
    "BatchIngestRequest",
    "BatchIngestResponse",
    "SingleIngestRequest",
    "SingleIngestResponse",
    "BatchStatusResponse",
    "ingest_router",
]

