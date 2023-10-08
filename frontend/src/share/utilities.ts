//const server = 'http://localhost:5000';
const server = '';


function switchPage(
  hasPage: boolean, 
  currPage: number, 
  action: string, 
  func: Function | null = null 
    ): void {
  
  if (hasPage) {
    action === 'previous' ? currPage -= 1 : currPage += 1
  }
  if (func) func();
};


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
  switchPage, 
  debounce,
  clearItem 
}
