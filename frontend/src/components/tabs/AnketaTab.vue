<script setup lang="ts">

import { ref, defineAsyncComponent } from 'vue';
import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';
import { clearItem } from '@utilities/utils'

const SwitchBtnForm = defineAsyncComponent(() => import('@components/elements/SwitchBtnForm.vue'));
const CollapseDiv = defineAsyncComponent(() => import('@components/elements/CollapseDiv.vue'));
const ResumeDiv = defineAsyncComponent(() => import('@components/tabs/divs/ResumeDiv.vue'));
const StaffDiv = defineAsyncComponent(() => import('@components/tabs/divs/StaffDiv.vue'));
const DocumentDiv = defineAsyncComponent(() => import('@components/tabs/divs/DocumentDiv.vue'));
const AddressDiv = defineAsyncComponent(() => import('@components/tabs/divs/AddressDiv.vue'));
const ContactDiv = defineAsyncComponent(() => import('@components/tabs/divs/ContactDiv.vue'));
const RelationDiv = defineAsyncComponent(() => import('@components/tabs/divs/RelationDiv.vue'));
const WorkplaceDiv = defineAsyncComponent(() => import('@components/tabs/divs/WorkplaceDiv.vue'));
const AffilationDiv = defineAsyncComponent(() => import('@components/tabs/divs/AffilationDiv.vue'));

import ResumeForm from '@components/forms/ResumeForm.vue';
import RegionForm from '@components/forms/RegionForm.vue';
import StaffForm from '@components/forms/StaffForm.vue';
import DocumentForm from '@components/forms/DocumentForm.vue';
import AddressForm from '@components/forms/AddressForm.vue';
import ContactForm from '@components/forms/ContactForm.vue';
import RelationForm from '@components/forms/RelationForm.vue';
import WorkplaceForm from '@components/forms/WorkplaceForm.vue';
import AffilationForm from '@components/forms/AffilationForm.vue';

const storeProfile = profileStore();
const storeClassify = classifyStore();

const hiddenSendBtn = ref(false);
const hiddenDelBtn = ref(false);

hiddenSendBtn.value = (storeProfile.dataProfile.resume['status'] 
                        !== storeClassify.classData.status['new'] 
                      && storeProfile.dataProfile.resume['status'] 
                        !== storeClassify.classData.status['update']
                      && storeProfile.dataProfile.resume['status'] 
                        !== storeClassify.classData.status['repeat']) 
                    || storeProfile.dataProfile.spinner

hiddenDelBtn.value = storeProfile.dataProfile.resume['status']
                       === storeClassify.classData.status['finish']
                    || storeProfile.dataProfile.spinner

function switchForm(item: string){
  storeProfile.dataProfile.flag === item 
    ? storeProfile.dataProfile.flag = '' 
    : storeProfile.dataProfile.flag = item;

  storeProfile.dataProfile.flag === item 
    ? storeProfile.dataProfile.action = 'create' 
    : storeProfile.dataProfile.action = ''; 

  clearItem(storeProfile.dataProfile.form)
};

</script>

<template>
  <div class="p-3">
  
    <template v-if="storeProfile.dataProfile.flag === 'resume' 
                 && storeProfile.dataProfile.action === 'update'" >
      <ResumeForm />
    </template>

    <template v-else>
      <RegionForm />
      <ResumeDiv v-if="storeProfile.dataProfile.resume"
                      :item="storeProfile.dataProfile.resume"
                      :regions="storeClassify.classData.regions"
                      :deleteItem="storeProfile.dataProfile.deleteItem"
                      :openForm="storeProfile.dataProfile.openForm"
                      :getItem="storeProfile.dataProfile.getItem"/>
        
      <p v-else >Данные отсутствуют</p>
    </template>
        
    <h6>Должности
      <SwitchBtnForm :item="'staff'" :switchForm="switchForm" 
                     :flag="storeProfile.dataProfile.flag"/>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'staff'">
      <StaffForm />
    </template>

    <template v-else>
      <div v-if="storeProfile.dataProfile.staffs">
        <CollapseDiv v-for="item, idx in storeProfile.dataProfile.needs" :key="idx" 
                            :id="item['id']" :idx="idx" :label="item['id']">
          <StaffDiv :item="item"
                    :deleteItem="storeProfile.dataProfile.deleteItem"
                    :openForm="storeProfile.dataProfile.openForm"/>
        </CollapseDiv>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Документы
      <SwitchBtnForm :item="'document'" :switchForm="switchForm" 
                     :flag="storeProfile.dataProfile.flag"/>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'document'">
      <DocumentForm />
    </template>
    
    <template v-else>
      <div v-if="storeProfile.dataProfile.docums">
        <CollapseDiv v-for="item, idx in storeProfile.dataProfile.docums" :key="idx" 
                            :id="item['id']" :idx="idx" :label="item['id']">
          <DocumentDiv :item="item"
                       :deleteItem="storeProfile.dataProfile.deleteItem"
                       :openForm="storeProfile.dataProfile.openForm"/>    
        </CollapseDiv>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>    

    <h6>Адреса
      <SwitchBtnForm :item="'address'" :switchForm="switchForm" 
                     :flag="storeProfile.dataProfile.flag"/>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'address'">
      <AddressForm />
    </template>
    
    <template v-else>
      <div v-if="storeProfile.dataProfile.addrs">
        <CollapseDiv v-for="item, idx in storeProfile.dataProfile.addrs" :key="idx" 
                            :id="item['id']" :idx="idx" :label="item['id']">
          <AddressDiv :item="item"
                      :deleteItem="storeProfile.dataProfile.deleteItem"
                      :openForm="storeProfile.dataProfile.openForm"/>  
        </CollapseDiv>
      </div>  
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Контакты
      <SwitchBtnForm :item="'contact'" :switchForm="switchForm" 
                     :flag="storeProfile.dataProfile.flag"/>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'contact'">
      <ContactForm />
    </template>
    
    <template v-else>
      <div v-if="storeProfile.dataProfile.conts">
        <CollapseDiv v-for="item, idx in storeProfile.dataProfile.conts" :key="idx" 
                            :id="item['id']" :idx="idx" :label="item['id']">
          <ContactDiv :item="item"
                      :deleteItem="storeProfile.dataProfile.deleteItem"
                      :openForm="storeProfile.dataProfile.openForm"/> 
        </CollapseDiv>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Работа
      <SwitchBtnForm :item="'workplace'" :switchForm="switchForm" 
                     :flag="storeProfile.dataProfile.flag"/>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'workplace'">
      <WorkplaceForm />
    </template>
    
    <template v-else>
      <div v-if="storeProfile.dataProfile.works">
        <CollapseDiv v-for="item, idx in storeProfile.dataProfile.works" :key="idx" 
                            :id="item['id']" :idx="idx" :label="item['id']">
          <WorkplaceDiv :item="item"
                        :deleteItem="storeProfile.dataProfile.deleteItem"
                        :openForm="storeProfile.dataProfile.openForm"/>
        </CollapseDiv>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Аффилированность
      <SwitchBtnForm :item="'affilation'" :switchForm="switchForm" 
                     :flag="storeProfile.dataProfile.flag"/>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'affilation'">
      <AffilationForm />
    </template>
    
    <template v-else>
      <div v-if="storeProfile.dataProfile.affilation">
        <CollapseDiv v-for="item, idx in storeProfile.dataProfile.affilation" :key="idx" 
                            :id="item['id']" :idx="idx" :label="item['id']">
          <AffilationDiv :item="item"
                        :deleteItem="storeProfile.dataProfile.deleteItem"
                        :openForm="storeProfile.dataProfile.openForm"/>
        </CollapseDiv>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Связи
      <SwitchBtnForm :item="'relation'" :switchForm="switchForm" 
                     :flag="storeProfile.dataProfile.flag"/>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'relation'">
      <RelationForm />
    </template>
    
    <template v-else>
      <div v-if="storeProfile.dataProfile.relate">
        <CollapseDiv v-for="item, idx in storeProfile.dataProfile.relate" :key="idx" 
                            :id="item['id']" :idx="idx" :label="item['id']">
          <RelationDiv :item="item"
                       :deleteItem="storeProfile.dataProfile.deleteItem"
                       :openForm="storeProfile.dataProfile.openForm"/>
        </CollapseDiv>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>

    <div class="py-3">
      <div class='btn-group' role="group">
        <button class="btn btn-outline-primary" 
                :disabled="hiddenSendBtn"
                @click="storeProfile.dataProfile.getItem('resume', 'send', storeProfile.dataProfile.candId)" >
            {{ !storeProfile.dataProfile.spinner ? 'Отправить на проверку' : '' }}
          <span v-if="storeProfile.dataProfile.spinner" class="spinner-border spinner-border-sm"></span>
          <span v-if="storeProfile.dataProfile.spinner" role="status">Отправляется...</span>
        </button>
        <button type="button" class="btn btn-outline-danger" 
                :disabled="hiddenDelBtn" 
                @click="storeProfile.dataProfile.deleteItem('resume', 'delete', 
                                                storeProfile.dataProfile.resume['id'])">
          Удалить анкету
        </button>
      </div>
    </div>
  </div>
</template>