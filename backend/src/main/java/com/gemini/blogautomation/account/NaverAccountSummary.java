package com.gemini.blogautomation.account;

import java.time.Instant;

public record NaverAccountSummary(
        String accountId,
        String displayName,
        String naverUserId,
        String blogId,
        boolean active,
        Instant createdAt
) {
    public static NaverAccountSummary from(NaverAccount account) {
        return new NaverAccountSummary(
                account.accountId(),
                account.displayName(),
                account.naverUserId(),
                account.blogId(),
                account.active(),
                account.createdAt()
        );
    }
}
