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
  await stateAnketa.getItem("contact");
});

const contact = ref({
  action: "",
  itemId: "",
  item: <Contact>{},
  showActions: false,
});

function submitForm(form: Object) {
  stateAnketa.updateItem(contact.value.action, "contact", contact.value.itemId, form);
  contact.value.action = "";
  contact.value.itemId = "";
  
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
    @cancel="contact.action = ''"
  />
  <div 
    v-if="stateAnketa.anketa.contact.length" 
    :class="{'collapse show': !stateAnketa.share.printPage}" 
    id="contact"
  > 
    <div 
      class="mb-3" 
      v-for="(item, idx) in stateAnketa.anketa.contact" :key="idx"
      @mouseover="contact.showActions = true"
      @mouseout="contact.showActions = false" 
      :class="{ 'card card-body': !stateAnketa.share.printPage }">
      <LabelSlot>
        <ActionIcons v-show="contact.showActions"
          @delete="stateAnketa.deleteItem(item['id'].toString(), 'contact')"
          @update="
            contact.action = 'update';
            contact.item = item;
            contact.itemId = item['id'].toString();
          "
        />
      </LabelSlot>
      <LabelSlot :label="'Вид'">{{ item['view'] }}</LabelSlot>
      <LabelSlot :label="'Контакт'">{{ item['contact'] }}</LabelSlot>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
