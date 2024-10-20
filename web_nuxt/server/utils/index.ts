import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import jwt from "jsonwebtoken";
import { eq } from "drizzle-orm";
import { db } from "~/server/db/index";
import { users } from "~/server/db/src/schema";

export const Roles = {
  admin: "admin",
  user: "user",
  guest: "guest",
};

export const Regions = {
  main: "Главный офис",
  south: "РЦ Юг",
  west: "РЦ Запад",
  ural: "РЦ Урал",
  east: "РЦ Восток",
};

export const Conclusions = {
  agreed: "Согласовано",
  comments: "Согласовано с комментарием",
  denied: "Отклонено",
};

export const JWT_SECRET_KEY = crypto.randomBytes(16).toString("hex");
export const SECRET_KEY = crypto.randomBytes(16).toString("hex");

export const currentUser =  async () => {
  const results = await db.select().from(users).where(eq(users.id, 2))
  return results[0];
}; // TODO: refactor

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

/**
 * Creates a folder for a given user in the specified region.
 * @param {string} region - The region to create the folder in.
 * @param {string} id - The id of the user.
 * @param {string} surname - The surname of the user.
 * @param {string} firstname - The firstname of the user.
 * @param {string} [patronymic] - The patronymic of the user.
 * @returns {string} The path of the created folder.
 */
export function makeDestinationFolder(
  region: string,
  id: string,
  surname: string,
  firstname: string,
  patronymic: string
): string {
  const folderName = path.join(
    process.env.DESTINATION as string,
    region,
    surname[0],
    `${id}-${surname} ${firstname} ${patronymic ? patronymic : ""}`
      .trim()
      .toUpperCase()
  );
  if (!fs.existsSync(folderName)) {
    fs.mkdirSync(folderName);
  }
  return folderName;
}
