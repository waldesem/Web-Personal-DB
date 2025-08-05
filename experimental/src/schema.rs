// @generated automatically by Diesel CLI.

diesel::table! {
    addresses (id) {
        id -> Integer,
        view -> Nullable<Text>,
        address -> Nullable<Text>,
        created -> Timestamp,
        person_id -> Integer,
    }
}

diesel::table! {
    affilations (id) {
        id -> Integer,
        view -> Nullable<Text>,
        organization -> Nullable<Text>,
        inn -> Nullable<Text>,
        created -> Timestamp,
        person_id -> Integer,
    }
}

diesel::table! {
    checks (id) {
        id -> Integer,
        workplace -> Nullable<Text>,
        document -> Nullable<Text>,
        inn -> Nullable<Text>,
        debt -> Nullable<Text>,
        bankruptcy -> Nullable<Text>,
        bki -> Nullable<Text>,
        courts -> Nullable<Text>,
        affilation -> Nullable<Text>,
        terrorist -> Nullable<Text>,
        mvd -> Nullable<Text>,
        internet -> Nullable<Text>,
        cronos -> Nullable<Text>,
        cros -> Nullable<Text>,
        addition -> Nullable<Text>,
        comment -> Nullable<Text>,
        conclusion -> Nullable<Text>,
        created -> Timestamp,
        person_id -> Integer,
    }
}

diesel::table! {
    contacts (id) {
        id -> Integer,
        view -> Nullable<Text>,
        contact -> Nullable<Text>,
        created -> Timestamp,
        person_id -> Integer,
    }
}

diesel::table! {
    documents (id) {
        id -> Integer,
        view -> Nullable<Text>,
        series -> Nullable<Text>,
        digits -> Nullable<Text>,
        agency -> Nullable<Text>,
        issue -> Nullable<Date>,
        created -> Timestamp,
        person_id -> Integer,
    }
}

diesel::table! {
    educations (id) {
        id -> Integer,
        view -> Nullable<Text>,
        institution -> Nullable<Text>,
        finished -> Nullable<Integer>,
        specialty -> Nullable<Text>,
        created -> Timestamp,
        person_id -> Integer,
    }
}

diesel::table! {
    inquiries (id) {
        id -> Integer,
        info -> Nullable<Text>,
        initiator -> Nullable<Text>,
        origins -> Nullable<Text>,
        created -> Timestamp,
        person_id -> Integer,
    }
}

diesel::table! {
    investigations (id) {
        id -> Integer,
        theme -> Nullable<Text>,
        info -> Nullable<Text>,
        created -> Timestamp,
        person_id -> Integer,
    }
}

diesel::table! {
    persons (id) {
        id -> Integer,
        surname -> Text,
        firstname -> Text,
        patronymic -> Nullable<Text>,
        birthday -> Date,
        birthplace -> Nullable<Text>,
        citizenship -> Nullable<Text>,
        dual -> Nullable<Text>,
        snils -> Nullable<Text>,
        inn -> Nullable<Text>,
        marital -> Nullable<Text>,
        addition -> Nullable<Text>,
        destination -> Nullable<Text>,
        created -> Timestamp,
        region -> Nullable<Text>,
        editable -> Bool,
        user_id -> Nullable<Integer>,
    }
}

diesel::table! {
    phones (id) {
        id -> Nullable<Integer>,
        organization -> Text,
        fullname -> Text,
        phone -> Nullable<Text>,
        mobile -> Nullable<Text>,
        email -> Nullable<Text>,
        comments -> Nullable<Text>,
        created -> Nullable<Timestamp>,
    }
}

diesel::table! {
    poligrafs (id) {
        id -> Integer,
        theme -> Nullable<Text>,
        results -> Nullable<Text>,
        created -> Timestamp,
        person_id -> Integer,
        conclusion -> Nullable<Text>,
    }
}

diesel::table! {
    previous (id) {
        id -> Integer,
        surname -> Nullable<Text>,
        firstname -> Nullable<Text>,
        patronymic -> Nullable<Text>,
        changed -> Nullable<Text>,
        reason -> Nullable<Text>,
        created -> Timestamp,
        person_id -> Integer,
    }
}

diesel::table! {
    staffs (id) {
        id -> Integer,
        position -> Nullable<Text>,
        department -> Nullable<Text>,
        created -> Timestamp,
        person_id -> Integer,
    }
}

diesel::table! {
    users (id) {
        id -> Integer,
        fullname -> Text,
        username -> Text,
        email -> Text,
        created -> Timestamp,
        passhash -> Text,
        pswd_create -> Timestamp,
        change_pswd -> Bool,
        blocked -> Bool,
        deleted -> Bool,
        attempt -> Integer,
        role -> Text,
    }
}

diesel::table! {
    workplaces (id) {
        id -> Integer,
        now_work -> Nullable<Bool>,
        starts -> Nullable<Date>,
        finished -> Nullable<Date>,
        workplace -> Nullable<Text>,
        address -> Nullable<Text>,
        position -> Nullable<Text>,
        reason -> Nullable<Text>,
        created -> Timestamp,
        person_id -> Integer,
    }
}

diesel::joinable!(addresses -> persons (person_id));
diesel::joinable!(affilations -> persons (person_id));
diesel::joinable!(checks -> persons (person_id));
diesel::joinable!(contacts -> persons (person_id));
diesel::joinable!(documents -> persons (person_id));
diesel::joinable!(educations -> persons (person_id));
diesel::joinable!(inquiries -> persons (person_id));
diesel::joinable!(investigations -> persons (person_id));
diesel::joinable!(persons -> users (user_id));
diesel::joinable!(poligrafs -> persons (person_id));
diesel::joinable!(previous -> persons (person_id));
diesel::joinable!(staffs -> persons (person_id));
diesel::joinable!(workplaces -> persons (person_id));

diesel::allow_tables_to_appear_in_same_query!(
    addresses,
    affilations,
    checks,
    contacts,
    documents,
    educations,
    inquiries,
    investigations,
    persons,
    phones,
    poligrafs,
    previous,
    staffs,
    users,
    workplaces,
);
