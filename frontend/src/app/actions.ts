"use server";

import { backend } from "@/apis";
import { ApiKey, UserRequest } from "@/types";

export const createApiKey = async ({ name }: { name: string }) => {
  try {
    const response = await backend.post<ApiKey>("/user/keys", {
      name: name,
    });
    return response.data;
  } catch (error) {
    console.log(error);
    return null;
  }
};

export const getApiKeys = async () => {
  try {
    const response = await backend.get<ApiKey[]>("/user/keys");
    return response.data;
  } catch (error) {
    console.log(error);
    return null;
  }
};

export const getUserRequests = async ({
    keyId
  }: {
    keyId: string
  }) => {
    try {
      const response = await backend.get<UserRequest[]>(`/user/keys/${keyId}/requests`, {
      });
      return response.data;
    } catch (error) {
      console.log(error);
      return null;
    }
  };
  
  
  
  



