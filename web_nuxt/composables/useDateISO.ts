/**
 * Преобразует дату в формат ISO (YYYY-MM-DD)
 * @param sourceRef - Реактивная ссылка на исходную дату (строка или null/undefined)
 * @param fallback - Значение по умолчанию при ошибке (по умолчанию "")
 */
export function useISODate(source: string | null | undefined, fallback = "") {
  const isValidDate = (value: string | null | undefined): value is string => {
    if (!value) return false;
    const date = new Date(value);
    return !isNaN(date.getTime());
  };

  const isoDate = computed(() => {
    if (!isValidDate(source)) return fallback;

    const date = new Date(source!);
    return date.toISOString().split('T')[0];
  });
  return isoDate;
}
