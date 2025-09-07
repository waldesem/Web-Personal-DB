import crypto from "node:crypto";

export const SECRET_KEY = crypto.randomBytes(16).toString("hex");

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
