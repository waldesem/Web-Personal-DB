export function capitalizeStr(str: string) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function localStr(str: string): string {
  return str ? new Date(str).toLocaleDateString() : "";
}

export function timeAgoStr(str: string) {
  const diff = Date.now() - new Date(str).getTime();
  const diffSeconds = Math.floor(diff / 1000);

  // Меньше минуты
  if (diffSeconds < 60) {
    return "менее минуты назад";
  }

  // Меньше часа (но больше минуты)
  const diffMinutes = Math.floor(diffSeconds / 60);
  if (diffMinutes < 60) {
    return diffMinutes + " минут назад";
  }

  // Менее суток (но больше часа)
  const diffHours = Math.floor(diffMinutes / 60);
  if (diffHours < 24) {
    return diffHours + " часов назад";
  }

  const diffDays = Math.floor(diffHours / 24);
  if (diffDays < 7) {
    return diffDays + " дней назад";
  }
  if (diffDays < 30) {
    return Math.floor(diffDays / 7) + " недели назад";
  }
  if (diffDays < 365) {
    return Math.floor(diffDays / 30) + " месяцев назад";
  }
  return Math.floor(diffDays / 365) + " года назад";
}
