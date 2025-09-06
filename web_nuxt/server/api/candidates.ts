export default defineEventHandler(async (event) => {
  const db = useDatabase();
  
  const data = JSON.parse(JSON.stringify(getQuery(event)));
  const perPage = parseInt(data.per_page as string);
  const page = parseInt(data.page as string);
  const search = data.search as string;

  // Базовый запрос
  let query = `
    SELECT 
      p.id, p.birthday, p.surname, p.firstname, p.patronymic,
      p.birthplace, p.citizenship, p.dual, p.snils, p.inn,
      p.marital, p.addition, p.destination, p.editable, p.created, p.user_id,
      u.fullname AS username,
      COUNT(*) OVER() AS total
    FROM persons p
    JOIN users u ON u.id = p.user_id
  `;
  const params: (string | number)[] = [];

  // Фильтрация по поиску
  if (search && search.length > 2) {
    const buffered = Buffer.from(search, "ascii").toString("utf-8");
    const searchData = buffered.toUpperCase().split(" ").slice(0, 3);
    
    query += " WHERE ";
    const conditions = [];
    
    if (searchData[0]) {
      conditions.push("surname LIKE ?");
      params.push(`%${searchData[0]}%`);
    }
    if (searchData[1]) {
      conditions.push("firstname LIKE ?");
      params.push(`%${searchData[1]}%`);
    }
    if (searchData[2]) {
      conditions.push("patronymic LIKE ?");
      params.push(`%${searchData[2]}%`);
    }
    
    query += conditions.join(" AND ");
  }

  // Сортировка и пагинация
  query += ` ORDER BY p.id DESC LIMIT ? OFFSET ?`;
  params.push(perPage, (page - 1) * perPage);

  // Выполнение запроса
  const stmt = db.prepare(query);
  return await stmt.all(...params);
});
