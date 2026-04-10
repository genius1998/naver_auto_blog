package com.gemini.blogautomation.account;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/accounts")
public class NaverAccountController {

    private final NaverAccountService accountService;

    public NaverAccountController(NaverAccountService accountService) {
        this.accountService = accountService;
    }

    @GetMapping
    public List<NaverAccountSummary> getAccounts() {
        return accountService.getAccounts();
    }

    @PostMapping
    public NaverAccountSummary createAccount(@Valid @RequestBody NaverAccountUpsertRequest request) {
        return accountService.createAccount(request);
    }
}
