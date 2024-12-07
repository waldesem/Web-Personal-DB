<script setup lang="ts">
import type { Work } from "@/types";

prefetchComponents("FormsWorkForm");

const emit = defineEmits(["message"]);

const authFetch = useFetchAuth();

const props = defineProps({
  candId: {
    type: String,
    default: "",
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

const collapse = ref(false);
const pending = ref(false);
const edit = ref(false);
const itemId = ref("");
const workplace = ref({} as Work);
const workplaces = ref<Work[]>([]);

const { refresh, status } = await useLazyAsyncData("workplaces", async () => {
  workplaces.value = (await authFetch(
    "/route/items/workplaces/" + props.candId
  )) as Work[];
});

async function submitWorkplace(form: Work) {
  closeAction();
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/workplaces/${props.candId}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  await refresh();
  emit("message", message);
}

async function deleteWork(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/workplaces/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  await refresh();
  emit("message", message);
}

function cancelOperation() {
  closeAction();
  refresh();
}

function closeAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    v-if="props.editable"
    :disabled="status == 'pending' || pending"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <ElementsCardDiv>
        <FormsWorkplaceForm
          :cand-id="props.candId"
          @cancel="cancelOperation"
          @update="submitWorkplace"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="workplaces && workplaces.length">
    <div v-for="(item, idx) in workplaces" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
      <ElementsCardDiv v-else>
        <FormsWorkplaceForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :work="workplace"
          @cancel="cancelOperation"
          @update="submitWorkplace"
        />
        <div v-else>
          <ElementsLabelSlot v-if="item['now_work']" :label="'Текущая работа'">
            {{ item["now_work"] ? "Да" : "Нет" }}
          </ElementsLabelSlot>
          <ElementsLabelSlot v-if="item['starts']" :label="'Начало работы'">
            {{
              new Date(item["starts"]).toLocaleDateString("ru-RU").split(",")[0]
            }}
          </ElementsLabelSlot>
          <ElementsLabelSlot
            v-if="item['finished']"
            :label="'Окончание работы'"
          >
            {{
              new Date(item["finished"])
                .toLocaleDateString("ru-RU")
                .split(",")[0]
            }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Место работы'">
            {{ item["workplace"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Адрес'">
            {{ item["addresses"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Должность'">
            {{ item["position"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot
            v-if="item['reason']"
            :label="'Причина увольнения'"
          >
            {{ item["reason"] }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :nav-items="3"
            @delete="deleteWork(item['id'])"
            @update="
              workplace = item;
              itemId = item['id'].toString();
              edit = true;
            "
            @upgrade="refresh()"
          />
        </template>
      </ElementsCardDiv>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
    <p v-else class="text-primary">Данные о работе отсутствуют</p>
  </div>
</template>
