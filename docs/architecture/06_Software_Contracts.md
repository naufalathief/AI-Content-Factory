ExperimentOrchestrator

Responsibility

Menjalankan experiment lifecycle.

Allowed Dependencies

Config
Trainer
Evaluator

Forbidden

Tidak boleh melakukan training.
Tidak boleh membaca dataset secara langsung.
Tidak boleh melakukan preprocessing.
Trainer

Responsibility

Melatih model.

Forbidden

Tidak boleh membuat model.
Tidak boleh membuat dataset.
Tidak boleh menghitung metric akhir.
Evaluator

Responsibility

Menghitung metric.

Forbidden

Tidak boleh training.
Tidak boleh update weight.
