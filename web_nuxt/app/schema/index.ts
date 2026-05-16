import * as v from "valibot";

export const schemaLogin = v.pipe(
  v.object({
    username: v.pipe(
      v.string(""),
      v.nonEmpty("Обязательное поле!"),
      v.maxLength(255, "Не более 255 символов!"),
    ),
    password: v.pipe(
      v.string(""),
      v.nonEmpty("Обязательное поле!"),
      v.maxLength(255, "Не более 255 символов!"),
    ),
  }),
);

export const schemaRegister = v.pipe(
  v.object({
    username: v.pipe(
      v.string(""),
      v.nonEmpty("Обязательное поле!"),
      v.maxLength(255, "Не более 255 символов!"),
    ),
    password: v.pipe(
      v.string(""),
      v.nonEmpty("Обязательное поле!"),
      v.maxLength(255, "Не более 255 символов!"),
    ),
    new_pswd: v.pipe(
      v.string(""),
      v.nonEmpty("Обязательное поле!"),
      v.regex(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$/,
        "От 8 до 16 символов, минимум 1 заглавная и 1 строчная буква и 1 цифра!",
      ),
    ),
    conf_pswd: v.pipe(v.string(""), v.nonEmpty("Обязательное поле!")),
  }),
  v.forward(
    v.check(
      (input) => input.password !== input.new_pswd,
      "Новый пароль не должен совпадать с текущим!",
    ),
    ["new_pswd"],
  ),
  v.forward(
    v.check(
      (input) => input.new_pswd === input.conf_pswd,
      "Новый пароль и подтверждение не совпадают!",
    ),
    ["conf_pswd"],
  ),
);
