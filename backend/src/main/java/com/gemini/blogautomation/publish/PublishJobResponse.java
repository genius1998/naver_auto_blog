package com.gemini.blogautomation.publish;

import java.time.Instant;

public record PublishJobResponse(
        String jobId,
        String blogId,
        String naverUserId,
        String keyword,
        String status,
        Instant requestedAt,
        String message,
        String publishUrl
) {
}
