package com.gemini.blogautomation.account;

import java.util.List;
import java.util.Optional;

public interface NaverAccountRepository {

    List<NaverAccount> findAll();

    Optional<NaverAccount> findById(String accountId);

    NaverAccount save(String accountId, NaverAccountUpsertRequest request);
}
