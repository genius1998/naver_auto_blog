package com.gemini.blogautomation.account;

import java.time.Instant;

public record NaverAccount(
        String accountId,
        String displayName,
        String naverUserId,
        String blogId,
        String cookiesRaw,
        boolean active,
        Instant createdAt
) {
}
