import { defineStore } from 'pinia';
import { ref, h } from 'vue';
//import { io } from 'socket.io-server';


export const chatStore = defineStore('chatStore', () => {

    const chatDialog = ref([{}]);
    const textInput =  ref('');
    
    function updateChat() {
      if (textInput.value == '') {
        return
      };
      chatDialog;
      textInput.value = '';
    };
    
    const chatBot = 
      h('div', [
        h('h3', 'StaffSecBot'),
        h('div', { class: 'py-3' }, [
          chatDialog.value.map((dialog: Object, index: number) =>
            h('div', {
              key: index,
              class: `badge bg-${Object.keys(dialog)[0] === 'chatbot' ? 'info' : 'success'} text-wrap`
            }, Object.values(dialog)[0])
          ),
          h('form', { on: { submit: updateChat }, class: 'form form-check', attrs: { role: 'form' } }, [
            h('div', { class: 'row' }, [
              h('div', { class: 'col-md-10' }, [
                h('textarea', {
                  class: 'form-control',
                  attrs: { id: 'chat', name: 'chat'},
                  domProps: { value: textInput },
                  on: { input: (event: { target: { value: string; }; }) => { 
                    textInput.value = event.target.value; 
                  } }
                })
              ]),
              h('div', { class: 'col-md-2' }, [
                h('button', { class: 'btn btn-outline-primary btn-sm', attrs: { type: 'submit', name: 'submit' } }, 'Отправить')
              ])
            ])
          ])
        ])
      ]);
    

  return { 
    chatBot, 
    textInput 
  }
});