import axios from "axios";

const TIMEOUT = 50 * 1000;

export const backend = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1`,
  headers: {
    "X-Api-Key": process.env.BACKEND_API_KEY,
  },
  timeout: TIMEOUT,
});
