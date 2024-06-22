<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Contact } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const ContactForm = defineAsyncComponent(
  () => import("@components/content/forms/ContactForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

onBeforeMount(async() => {
  await stateAnketa.getItem("contacts");
});

const contact = ref({
  action: "",
  itemId: "",
  item: <Contact>{},
  showActions: false,
});

function cancelAction(){
  contact.value.action = "";
  contact.value.itemId = "";
  contact.value.item = <Contact>({});
};

function submitForm(form: Object) {
  stateAnketa.updateItem("contacts", form);
  cancelAction();
};
</script>

<template>
  <ActionHeader
    :id="'contact'"
    :header="'Контакты'"
    :action="contact.action"
    @action="contact.action = contact.action ? '' : 'create'"
  />
  <ContactForm v-if="contact.action === 'create'"
    :contact="contact.item" 
    @submit="submitForm" 
    @cancel="cancelAction"
  />
  <div 
    v-if="stateAnketa.anketa.contacts.length" 
    class="collapse show" 
    id="contact"
  > 
    <div 
      v-for="(item, idx) in stateAnketa.anketa.contacts" :key="idx"
      @mouseover="contact.showActions = true"
      @mouseout="contact.showActions = false" 
      class="card card-body mb-3"
    >
      <ContactForm
        v-if="
          contact.action === 'update' &&
          contact.itemId === item['id'].toString()
        "
        :contact="contact.item"
        @submit="submitForm"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons v-show="contact.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'contacts')"
            @update="
              contact.action = 'update';
              contact.item = item;
              contact.itemId = item['id'].toString();
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Вид'">{{ item['view'] }}</LabelSlot>
        <LabelSlot :label="'Контакт'">{{ item['contact'] }}</LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
