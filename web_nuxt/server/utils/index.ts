import crypto from "node:crypto";
import jwt from "jsonwebtoken";

export const Roles = {
  admin: "admin",
  user: "user",
  guest: "guest",
}

export const Regions = {
  main: "Главный офис",
  south: "РЦ Юг",
  west: "РЦ Запад",
  ural: "РЦ Урал",
  east: "РЦ Восток",
}

export const Conclusions = {
  agreed: "Согласовано",
  comments: "Согласовано с комментарием",
  denied: "Отклонено",
}

export const JWT_SECRET_KEY = crypto.randomBytes(16).toString("hex");

/**
 * Creates a password hash using the crypto module.
 * @param {string} password - The password to hash.
 * @returns {string} The hashed password.
 */
export function createPasswordHash(password: string): string {
  const salt = crypto.randomBytes(16).toString("hex");
  const hash = crypto.createHmac("sha256", salt);
  hash.update(password);
  return `${salt}:${hash.digest("hex")}`;
}

/**
 * Checks a password against a stored hash.
 * @param {string} password - The password to check.
 * @param {string} hash - The stored hash.
 * @returns {boolean} True if the password matches the hash, false otherwise.
 */
export function checkPasswordHash(password: string, hash: string): boolean {
  const [salt, storedHash] = hash.split(":");
  const newHash = crypto.createHmac("sha256", salt);
  newHash.update(password);
  return newHash.digest("hex") === storedHash;
}

/**
 * Creates a JWT token with the given payload and secret.
 * @param {Object} payload - The payload to include in the token.
 * @param {string} secret - The secret key to sign the token with.
 * @param {Object} [options] - Additional options for the token.
 * @returns {string} The JWT token.
 */
export function createJwtToken(
  payload: object,
  secret: string,
  options: object = {}
): string {
  return jwt.sign(payload, secret, options);
}
