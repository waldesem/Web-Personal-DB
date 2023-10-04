
function debounce(func: (...args: any[]) => void, delay: number): (...args: any[]) => void {
    let timer: ReturnType<typeof setTimeout> | undefined;
  
    return function(this: any, ...args: any[]) {
      if (timer) clearTimeout(timer);
  
      timer = setTimeout(() => {
        func.apply(this, args);
        timer = undefined; // Reset the timer after the function is called
      }, delay);
    };
  };

export default debounce