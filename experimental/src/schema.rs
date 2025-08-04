table! {
    users (id) {
        id -> Int4,
        fullname -> Varchar,
        username -> Varchar,
        email -> Varchar,
        created -> Timestamptz,
        passhash -> Varchar,
        pswd_create -> Timestamptz,
        change_pswd -> Bool,
        blocked -> Bool,
        deleted -> Bool,
        attempt -> Int4,
        role -> Varchar,
    }
}

table! {
    persons (id) {
        id -> Int4,
        surname -> Varchar,
        firstname -> Varchar,
        patronymic -> Nullable<Varchar>,
        birthday -> Date,
        birthplace -> Text,
        citizenship -> Nullable<Varchar>,
        dual -> Nullable<Varchar>,
        snils -> Nullable<Varchar>,
        inn -> Nullable<Varchar>,
        marital -> Nullable<Varchar>,
        addition -> Nullable<Text>,
        destination -> Nullable<Text>,
        created -> Timestamptz,
        editable -> Bool,
        user_id -> Nullable<Int4>,
    }
}
