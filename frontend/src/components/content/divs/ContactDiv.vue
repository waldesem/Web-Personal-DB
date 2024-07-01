<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa } from "@/state";
import { Contact } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const ContactForm = defineAsyncComponent(
  () => import("@components/content/forms/ContactForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const contact = ref({
  itemId: "",
  item: <Contact>{},
  showActions: false,
});

function cancelAction(){
  contact.value.itemId = "";
  Object.keys(contact.value.item).forEach(
    (key) => delete contact.value.item[key as keyof typeof contact.value.item]
  );
  const collapseContact = document.getElementById('contact');
  collapseContact?.setAttribute('class', 'collapse card card-body');
};
</script>

<template>
  <DropDownHead :id="'contact'" :header="'Контакты'"/>
  <div class="collapse card card-body" id="contact">
    <ContactForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.contacts.length"> 
    <div 
      v-for="(item, idx) in stateAnketa.anketa.contacts" :key="idx"
      @mouseover="contact.showActions = true"
      @mouseout="contact.showActions = false" 
      class="card card-body"
    >
      <ContactForm
        v-if="contact.itemId === item['id'].toString()"
        :contact="contact.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons v-show="contact.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'contacts')"
            @update="
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

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>