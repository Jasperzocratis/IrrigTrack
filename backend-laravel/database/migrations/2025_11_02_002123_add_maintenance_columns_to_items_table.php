<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('items', function (Blueprint $table) {
            $table->integer('maintenance_count')->default(0)->after('status'); // increments every maintenance
            $table->float('lifespan_estimate')->nullable()->after('maintenance_count'); // predicted total lifespan (years)
            $table->float('remaining_years')->nullable()->after('lifespan_estimate'); // predicted remaining years
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('items', function (Blueprint $table) {
            $table->dropColumn(['maintenance_count', 'lifespan_estimate', 'remaining_years']);
        });
    }
};
