<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
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

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(() => {
  emit("get-item");
});

const props = defineProps({
  printPage: {
    type: Boolean,
    default: false,
  },
  items: {
    type: Array as () => Array<Contact>,
    default: {},
  },
});

const contact = ref({
  action: "",
  itemId: "",
  item: <Contact>{},
  showActions: false,
});

function submitForm(form: Object) {
  emit("submit", contact.value.action, "contact", contact.value.itemId, form);
  contact.value.action = "";
};
</script>

<template>
  <ActionHeader
    :print-page="props.printPage"
    :id="'contact'"
    :header="'Контакты'"
    :action="contact.action"
    @action="contact.action = contact.action ? '' : 'create'"
  />
  <ContactForm v-if="contact.action"
    :contact="contact.item" 
    @submit="submitForm" 
    @cancel="contact.action = ''"
  />
  <div v-else
    @mouseover="contact.showActions = true"
    @mouseout="contact.showActions = false"
  >
    <div 
      v-if="props.items.length" 
      :class="{'collapse show': !printPage}" 
      id="contact"
    > 
      <div class="mb-3" v-for="(item, idx) in props.items" :key="idx">
        <div class="card card-body">
          <LabelSlot>
            <ActionIcons v-show="contact.showActions"
              @delete="emit('delete', item['id'].toString(), 'contact')"
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
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
