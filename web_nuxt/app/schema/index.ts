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

export const schemaName = v.object({
  surname: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.regex(
      /^[А-ЯЁа-яё][А-ЯЁа-яёIV\-.,'()\s]*[А-ЯЁа-яё]$|^[А-ЯЁа-яё]$/,
      "Недопустимые символы!",
    ),
    v.maxLength(255, "Не более 255 символов!"),
  ),
  firstname: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.regex(
      /^[А-ЯЁа-яё][А-ЯЁа-яёIV\-.,'()\s]*[А-ЯЁа-яё]$|^[А-ЯЁа-яё]$/,
      "Недопустимые символы!",
    ),
    v.maxLength(255, "Не более 255 символов!"),
  ),
  patronymic: v.pipe(
    v.string(),
    v.check(
      (value) =>
        value === "" ||
        /^[А-ЯЁа-яё][А-ЯЁа-яёIV\-.,'()\s]*[А-ЯЁа-яё]$|^[А-ЯЁа-яё]$/.test(value),
      "Недопустимые символы!",
    ),
    v.maxLength(255, "Не более 255 символов!"),
  ),
});

export const schemaResume = v.intersect([
  schemaName,
  v.object({
    birthday: v.pipe(
      v.string(),
      v.nonEmpty("Обязательное поле!"),
      v.toDate(),
      v.maxValue(new Date(), "Дата находится в будущем!"),
      v.minValue(new Date(1900, 0, 1), "Дата слишком старая!"),
    ),
    birthplace: v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
    citizenship: v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
    dual: v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
    snils: v.pipe(
      v.string(),
      v.check(
        (value) => value === "" || /^\d{11}$/.test(value),
        "Должно быть 11 цифр!",
      ),
    ),
    inn: v.pipe(
      v.string(),
      v.check(
        (value) => value === "" || /^\d{12}$/.test(value),
        "Должно быть 12 цифр!",
      ),
    ),
    marital: v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
    addition: v.pipe(v.string(), v.maxLength(4096, "Не более 4096 символов!")),
  }),
]);

export const schemaPrevious = v.intersect([
  schemaName,
  v.object({
    changed: v.pipe(
      v.string(),
      v.check(
        (value) => value === "" || /^\d{4}$/.test(value),
        "Должно быть 4 цифры!",
      ),
    ),
    reason: v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
  }),
]);

export const schemaDoc = v.object({
  view: v.pipe(
    v.string(),
    v.union([
      v.literal("Паспорт"),
      v.literal("Иностранный паспорт"),
      v.literal("Другое"),
    ]),
  ),
  series: v.pipe(v.string(), v.maxLength(255)),
  digits: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.regex(/^\d{1,12}$/, "Недопустимые символы!"),
  ),
  agency: v.pipe(v.string(), v.maxLength(255)),
  issue: v.pipe(
    v.string(),
    v.toDate(),
    v.maxValue(new Date(), "Дата находится в будущем!"),
    v.minValue(new Date(1900, 0, 1), "Дата слишком старая!"),
  ),
});

export const schemaWork = v.object({
  starts: v.pipe(
    v.string(),
    v.toDate(),
    v.minValue(new Date(1900, 0, 1), "Дата слишком старая!"),
  ),
  finished: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.toDate(),
    v.minValue(new Date(1900, 0, 1), "Дата слишком старая!"),
  ),
  workplace: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.maxLength(255, "Не более 255 символов!"),
  ),
  position: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.maxLength(255, "Не более 255 символов!"),
  ),
  address: v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
  reason: v.pipe(v.string(), v.maxLength(4096, "Не более 4096 символов!")),
});
