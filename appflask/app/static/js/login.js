'use strict';

let loginAction = 'create';
let showPswd = false;

const switchAction = () => {
    return loginAction = loginAction === 'create' ? 'update' : 'create';
}
