package com.gemini.blogautomation.publish;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.time.Instant;
import java.util.Map;
import java.util.UUID;

@Service
public class PublishService {

    private final ObjectMapper objectMapper;

    @Value("${app.publisher.python-command:python}")
    private String pythonCommand;

    @Value("${app.publisher.script-path:publisher_cli.py}")
    private String scriptPath;

    @Value("${app.publisher.working-directory:..}")
    private String workingDirectory;

    @Value("${app.publisher.gemini-api-key:#{systemEnvironment['GEMINI_API_KEY'] ?: ''}}")
    private String geminiApiKey;

    public PublishService(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public PublishJobResponse createPublishJob(PublishJobRequest request) {
        String jobId = UUID.randomUUID().toString();
        Instant requestedAt = Instant.now();

        if (geminiApiKey == null || geminiApiKey.isBlank()) {
            throw new IllegalStateException("GEMINI_API_KEY is not configured");
        }

        try {
            Map<String, Object> publishResult = runPublisher(request);
            String redirectUrl = extractRedirectUrl(publishResult);

            return new PublishJobResponse(
                    jobId,
                    request.blogId(),
                    request.naverUserId(),
                    request.keyword(),
                    "PUBLISHED",
                    requestedAt,
                    "Publish completed successfully.",
                    redirectUrl
            );
        } catch (Exception exception) {
            return new PublishJobResponse(
                    jobId,
                    request.blogId(),
                    request.naverUserId(),
                    request.keyword(),
                    "FAILED",
                    requestedAt,
                    exception.getMessage(),
                    null
            );
        }
    }

    private Map<String, Object> runPublisher(PublishJobRequest request) throws IOException, InterruptedException {
        ProcessBuilder processBuilder = new ProcessBuilder(pythonCommand, scriptPath);
        processBuilder.directory(resolveWorkingDirectory().toFile());

        Process process = processBuilder.start();

        Map<String, String> payload = Map.of(
                "geminiApiKey", geminiApiKey,
                "blogId", request.blogId(),
                "naverUserId", request.naverUserId(),
                "cookiesRaw", request.cookiesRaw(),
                "keyword", request.keyword()
        );

        try (Writer writer = new OutputStreamWriter(process.getOutputStream(), StandardCharsets.UTF_8)) {
            objectMapper.writeValue(writer, payload);
        }

        String stdout = new String(process.getInputStream().readAllBytes(), StandardCharsets.UTF_8).trim();
        String stderr = new String(process.getErrorStream().readAllBytes(), StandardCharsets.UTF_8).trim();
        int exitCode = process.waitFor();

        if (exitCode != 0) {
            throw new IllegalStateException(stderr.isBlank() ? "Publisher process failed" : stderr);
        }
        if (stdout.isBlank()) {
            throw new IllegalStateException("Publisher process returned an empty response");
        }

        return objectMapper.readValue(stdout, new TypeReference<>() {});
    }

    private Path resolveWorkingDirectory() {
        Path backendDir = Path.of("").toAbsolutePath();
        return backendDir.resolve(workingDirectory).normalize();
    }

    private String extractRedirectUrl(Map<String, Object> publishResult) {
        Object result = publishResult.get("result");
        if (!(result instanceof Map<?, ?> resultMap)) {
            return "";
        }
        Object redirectUrl = resultMap.get("redirectUrl");
        return redirectUrl == null ? "" : redirectUrl.toString();
    }
}
