import { ref } from 'vue';

interface Resume {
    id: string;
    category: string;
    region_id: string;
    fullname: string;
    previous: string;
    birthday: string;
    birthplace: string;
    country: string;
    snils: string;
    inn: string;
    education: string;
    addition: string;
    path: string;
    status: string;
    create: string;
    update: string;
    request_id: string;
  }
  
  interface Document {
    id: string;
    view: string;
    series: string;
    number: string;
    agency: string;
    issue: string;
  }
  
  interface Address {
    id: string;
    view: string;
    region: string;
    address: string;
  }
  
  interface Contact {
    id: string;
    view: string;
    contact: string;
  }
  
  interface Work {
    id: string;
    start_date: string;
    end_date: string;
    workplace: string;
    address: string;
    position: string;
  }
  
  interface Staff {
    id: string;
    position: string;
    department: string;
  }
  
  interface Relation {
    id: string;
    relation: string;
    relation_id: string;
  }
  
  interface Verification {
    id: string;
    workplace: string;
    employee: string;
    document: string;
    inn: string;
    debt: string;
    bankruptcy: string;
    bki: string;
    courts: string;
    affiliation: string;
    terrorist: string;
    mvd: string;
    internet: string;
    cronos: string;
    cros: string;
    addition: string;
    pfo: boolean;
    conclusion: string;
    comments: string;
    deadline: string;
    officer: string;
  }
  
  interface Register {
    id: string;
    comments: string;
    decision: string;
    supervisor: string;
    deadline: string;
  }
  
  interface Pfo {
    id: string;
    theme: string;
    results: string;
    officer: string;
    deadline: string;
  }
  
  interface Inquisition {
    id: string;
    theme: string;
    info: string;
    officer: string;
    deadline: string;
  }
  
  interface Needs {
    id: string;
    info: string;
    initiator: string;
    source: string;
    officer: string;
    deadline: string;
  }
  
  const anketa = ref<{
    resume: Resume;
    docums: Document[];
    addrs: Address[];
    conts: Contact[];
    works: Work[];
    staffs: Staff[];
    relate: Relation[];
  }>({
    resume: {
      id: '',
      category: '',
      region_id: '',
      fullname: '',
      previous: '',
      birthday: '',
      birthplace: '',
      country: '',
      snils: '',
      inn: '',
      education: '',
      addition: '',
      path: '',
      status: '',
      create: '',
      update: '',
      request_id: '',
    },
    docums: [{
      id: '',
      view: '',
      series: '',
      number: '',
      agency: '',
      issue: '',
    }],
    addrs: [{
      id: '',
      view: '',
      region: '',
      address: '',
    }],
    conts: [{
      id: '',
      view: '',
      contact: '',
    }],
    works: [{
      id: '',
      start_date: '',
      end_date: '',
      workplace: '',
      address: '',
      position: '',
    }],
    staffs: [{
      id: '',
      position: '',
      department: ''
    }],
    relate: [{
      id: '',
      relation: '',
      relation_id: ''
    }]
  });
  
  const verification = ref<Verification[]>([{
    id: '',
    workplace: '', 
    employee: '', 
    document: '', 
    inn: '', 
    debt: '', 
    bankruptcy: '', 
    bki: '', 
    courts: '', 
    affiliation: '', 
    terrorist: '', 
    mvd: '', 
    internet: '', 
    cronos: '', 
    cros: '', 
    addition: '', 
    pfo: false, 
    conclusion: '', 
    comments: '', 
    deadline: '', 
    officer: '',
 }]);

    
  const register = ref<Register[]>([{
    id: '',
    comments: '',
    decision: '',
    supervisor: '',
    deadline: '',
  }]);

  const pfo = ref<Pfo[]>([{
    id: '',
    theme: '',
    results: '',
    officer: '',
    deadline: '',
  }]);

  const inquisition = ref<Inquisition[]>([{
    id: '',
    theme: '',
    info: '',
    officer: '',
    deadline: ''
  }]);
  
  const needs = ref<Needs[]>([{
    id: '',
    info: '',
    initiator: '',
    source: '',
    officer: '',
    deadline: '',
  }]);

export { anketa, verification, register, pfo, inquisition, needs }


  // const anketa = ref({
  // resume: {
  //     id: '',
  //     category: '',
  //     region_id: '',
  //     fullname: '',
  //     previous: '',
  //     birthday: '',
  //     birthplace: '',
  //     country: '',
  //     snils: '',
  //     inn: '',
  //     education: '',
  //     addition: '',
  //     path: '',
  //     status: '',
  //     create: '',
  //     update: '',
  //     request_id: '',
  //   },
  //   docums: [{
  //     id: '',
  //     view: '',
  //     series: '',
  //     number: '',
  //     agency: '',
  //     issue: '',
  //   }],
  //   addrs: [{
  //     id: '',
  //     view: '',
  //     region: '',
  //     address: '',
  //   }],
  //   conts: [{
  //     id: '',
  //     view: '',
  //     contact: '',
  //   }],
  //   works: [{
  //     id: '',
  //     start_date: '',
  //     end_date: '',
  //     workplace: '',
  //     address: '',
  //     position: '',
  //   }],
  //   staffs: [{
  //     id: '',
  //     position: '',
  //     department: ''
  //   }],
  //   relate: [{
  //     id: '',
  //     relation: '',
  //     relation_id: ''
  //   }]
  // });
  
  // const verification = ref([{
  //   id: '',
  //   workplace: '',
  //   employee: '',
  //   document: '',
  //   inn: '',
  //   debt: '',
  //   bankruptcy: '',
  //   bki: '',
  //   courts: '',
  //   affiliation: '',
  //   terrorist: '',
  //   mvd: '',
  //   internet: '',
  //   cronos: '',
  //   cros: '',
  //   addition: '',
  //   pfo: false,
  //   conclusion: '',
  //   comments: '',
  //   deadline: '',
  //   officer: '',
  // }]);

  // const register = ref([{
  //   id: '',
  //   comments: '',
  //   decision: '',
  //   supervisor: '',
  //   deadline: '',
  // }]);

  // const pfo = ref([{
  //   id: '',
  //   theme: '',
  //   results: '',
  //   officer: '',
  //   deadline: '',
  // }]);

  // const inquisition = ref([{
  //   id: '',
  //   theme: '',
  //   info: '',
  //   officer: '',
  //   deadline: ''
  // }]);
  
  // const needs = ref([{
  //   id: '',
  //   info: '',
  //   initiator: '',
  //   source: '',
  //   officer: '',
  //   deadline: '',
  // }]);