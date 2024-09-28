/**
 * Get the user token from ref.
*/
export const userToken = ref("");

/**
 * Debounces a function, ensuring it's not called again until a certain amount of time has passed.
 *
 * @param {Function} func - The function to be debounced
 * @param {number} delay - The delay in milliseconds
 * @return {Function} - The debounced function
 */
export function debounce(
  func: (...args: unknown[]) => void,
  delay: number
): (...args: unknown[]) => void {
  let timer: ReturnType<typeof setTimeout> | undefined;

  return function (this: unknown, ...args: unknown[]) {
    if (timer) clearTimeout(timer);

    timer = setTimeout(() => {
      func.apply(this, args);
      timer = undefined; // Reset the timer after the function is called
    }, delay);
  };
}

