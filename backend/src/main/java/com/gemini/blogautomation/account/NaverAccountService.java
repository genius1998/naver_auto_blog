package com.gemini.blogautomation.account;

import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NaverAccountService {

    private final NaverAccountRepository repository;

    public NaverAccountService(NaverAccountRepository repository) {
        this.repository = repository;
    }

    public List<NaverAccountSummary> getAccounts() {
        return repository.findAll().stream()
                .map(NaverAccountSummary::from)
                .toList();
    }

    public NaverAccount getAccount(String accountId) {
        return repository.findById(accountId)
                .orElseThrow(() -> new IllegalArgumentException("Account not found: " + accountId));
    }

    public NaverAccountSummary createAccount(NaverAccountUpsertRequest request) {
        return NaverAccountSummary.from(repository.save(null, request));
    }
}
