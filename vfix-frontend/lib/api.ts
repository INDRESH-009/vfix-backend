"use client";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE!;

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("jwt");
}

export function setToken(jwt: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem("jwt", jwt);
}

export function clearToken() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("jwt");
}

export async function apiGET<T>(path: string): Promise<T> {
  const token = getToken();
  const res = await fetch(`${API_BASE}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    cache: "no-store",
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiPOST<T>(path: string, body: any, isJSON = true): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {};
  if (isJSON) headers["Content-Type"] = "application/json";
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers,
    body: isJSON ? JSON.stringify(body) : body,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
