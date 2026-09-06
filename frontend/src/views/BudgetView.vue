<script setup>
import BudgetSettingsCard from '../components/BudgetSettingsCard.vue'
import PageShell from '../components/PageShell.vue'
import PageTitle from '../components/PageTitle.vue'
</script>

<template>
  <PageShell>
    <template #sticky>
      <PageTitle text="Ngân sách" />
    </template>

    <BudgetSettingsCard />
  </PageShell>
</template>
