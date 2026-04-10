package com.gemini.blogautomation.account;

import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class InMemoryNaverAccountRepository implements NaverAccountRepository {

    private final ConcurrentHashMap<String, NaverAccount> storage = new ConcurrentHashMap<>();

    @Override
    public List<NaverAccount> findAll() {
        return storage.values().stream()
                .sorted(Comparator.comparing(NaverAccount::createdAt))
                .toList();
    }

    @Override
    public Optional<NaverAccount> findById(String accountId) {
        return Optional.ofNullable(storage.get(accountId));
    }

    @Override
    public NaverAccount save(String accountId, NaverAccountUpsertRequest request) {
        String resolvedId = accountId == null || accountId.isBlank() ? UUID.randomUUID().toString() : accountId;
        Instant createdAt = Optional.ofNullable(storage.get(resolvedId))
                .map(NaverAccount::createdAt)
                .orElseGet(Instant::now);

        NaverAccount account = new NaverAccount(
                resolvedId,
                request.displayName(),
                request.naverUserId(),
                request.blogId(),
                request.cookiesRaw(),
                request.active(),
                createdAt
        );
        storage.put(resolvedId, account);
        return account;
    }
}
