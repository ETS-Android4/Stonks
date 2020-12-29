package com.example.stonks_.api;

import com.example.stonks_.models.news;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface News_ApiInterface {
    @GET("everything")
    Call<news> getnews(
            @Query("q") String querry,
            @Query("language") String language,
            @Query("apiKey") String apiKey
    );
}

