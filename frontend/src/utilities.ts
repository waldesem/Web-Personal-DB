/**
 * Debounces a function, ensuring it's not called again until a certain amount of time has passed.
 *
 * @param {Function} func - The function to be debounced
 * @param {number} delay - The delay in milliseconds
 * @return {Function} - The debounced function
 */
export function debounce(
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
