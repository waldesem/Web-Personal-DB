const server = "http://localhost:5000";
// const server = '';

/**
 * Debounces a function, ensuring it's not called again until a certain amount of time has passed.
 *
 * @param {Function} func - The function to be debounced
 * @param {number} delay - The delay in milliseconds
 * @return {Function} - The debounced function
 */
function debounce(
  func: (...args: any[]) => void,
  delay: number
): (...args: any[]) => void {
  let timer: ReturnType<typeof setTimeout> | undefined;

  return function (this: any, ...args: any[]) {
    if (timer) clearTimeout(timer);

    timer = setTimeout(() => {
      func.apply(this, args);
      timer = undefined; // Reset the timer after the function is called
    }, delay);
  };
}

/**
 * Calculates the time interval since the given date and returns a human-readable string representing the time elapsed.
 *
 * @param {string} date - The date to calculate the time since
 * @return {string} A string representing the time elapsed in a human-readable format
 */
function timeSince(date: string): string {
  let seconds =
    (new Date().getTime() -
      new Date(date).getTime() +
      new Date().getTimezoneOffset() * 60000) /
    1000;
  let interval = seconds / 31536000;
  if (interval > 1) {
    return Math.floor(interval) + " лет назад";
  }
  interval = seconds / 2592000;
  if (interval > 1) {
    return Math.floor(interval) + " месяцев назад";
  }
  interval = seconds / 86400;
  if (interval > 1) {
    return Math.floor(interval) + " дней назад";
  }
  interval = seconds / 3600;
  if (interval > 1) {
    return Math.floor(interval) + " часов назад";
  }
  interval = seconds / 60;
  if (interval > 1) {
    return Math.floor(interval) + " минут назад";
  }
  return Math.floor(seconds) + " секунд назад";
}

export { server, debounce, timeSince };
