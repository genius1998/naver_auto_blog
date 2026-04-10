package com.gemini.blogautomation.publish;

import jakarta.validation.constraints.NotBlank;

public record PublishJobRequest(
        @NotBlank String blogId,
        @NotBlank String naverUserId,
        @NotBlank String cookiesRaw,
        @NotBlank String keyword
) {
}
