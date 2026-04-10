package com.gemini.blogautomation.account;

import jakarta.validation.constraints.NotBlank;

public record NaverAccountUpsertRequest(
        @NotBlank String displayName,
        @NotBlank String naverUserId,
        @NotBlank String blogId,
        @NotBlank String cookiesRaw,
        boolean active
) {
}
