export function localStr(str: string): string {
  try {
    return str ? new Date(str).toLocaleDateString() : "";
  } catch (e) {
    console.error(e);
    return "";
  }
}

export function timeAgoStr(str: string) {
  const diff = Date.now() - new Date(str).getTime();
  const diffSec = Math.floor(diff / 1000);

  // Меньше минуты
  if (diffSec < 60) {
    return "менее минуты назад";
  }

  // Меньше часа (но больше минуты)
  const diffMin = Math.floor(diffSec / 60);
  if (diffMin < 60) {
    return diffMin + " минут назад";
  }

  // Менее суток (но больше часа)
  const diffHours = Math.floor(diffMin / 60);
  if (diffHours < 24) {
    return diffHours + " часов назад";
  }

  const diffDays = Math.floor(diffHours / 24);
  // Менее недели (но больше суток)
  if (diffDays < 7) {
    return diffDays + " дней назад";
  }

  if (diffDays < 30) {
    // Менее месяца (но больше недели)
    return Math.floor(diffDays / 7) + " недели назад";
  }

  // Менее года (но больше месяца)
  if (diffDays < 365) {
    return Math.floor(diffDays / 30) + " месяцев назад";
  }

  // Больше года
  return Math.floor(diffDays / 365) + " года назад";
}
