const server = 'http://localhost:5000';
//const server = '';

function debounce(
  func: (...args: any[]) => void, 
  delay: number): (...args: any[]
    ) => void {

  let timer: ReturnType<typeof setTimeout> | undefined;

  return function(this: any, ...args: any[]) {
    if (timer) clearTimeout(timer);

    timer = setTimeout(() => {
      func.apply(this, args);
      timer = undefined; // Reset the timer after the function is called
    }, delay);
  };
};


function clearItem(item: Object): void {
  Object.keys(item).forEach(key => {
    delete item[key as keyof typeof item];
  });
};
  
export { 
  server, 
  debounce,
  clearItem 
}
