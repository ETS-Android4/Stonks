package com.example.stonks_.models;

import com.google.gson.annotations.SerializedName;

import org.json.JSONObject;

import java.util.List;

public class news {

    @SerializedName("status")
    private String status;

    @SerializedName("articles")
    private List<Articles> data;

    @SerializedName("totalResults")
    private int total;

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public List<Articles> getData() {
        return data;
    }

    public void setData(List<Articles> data) {
        this.data = data;
    }

    public int getTotal() {
        return total;
    }

    public void setTotal(int total) {
        this.total = total;
    }
}
