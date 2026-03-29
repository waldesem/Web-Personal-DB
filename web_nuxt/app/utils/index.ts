export function capitalize(str: string) {
  if (typeof str == "string") return str.charAt(0).toUpperCase() + str.slice(1);
  else return "";
}

export function workExperience(
  starts: string,
  finished: string,
  created: string,
) {
  const duration = {
    years: 0,
    months: 0,
    days: 0,
  };
  const end = finished ? new Date(finished) : new Date(created);
  if (!starts) {
    return duration;
  }
  const start = new Date(starts);

  duration.years = end.getFullYear() - start.getFullYear();
  duration.months = end.getMonth() - start.getMonth();
  duration.days = end.getDate() - start.getDate();

  // Коррекция дней, если конечная дата меньше начальной по дням
  if (duration.days < 0) {
    duration.months--;
    const lastDayOfPrevMonth = new Date(
      end.getFullYear(),
      end.getMonth(),
      0,
    ).getDate();
    duration.days += lastDayOfPrevMonth;
  }

  // Коррекция месяцев, если они отрицательные
  if (duration.months < 0) {
    duration.years--;
    duration.months += 12;
  }

  return duration;
}
