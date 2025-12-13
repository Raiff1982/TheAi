# Insert this at the top of your file
from unicode_threat_analyzer import detect_unicode_threat

# Then add this block to the beginning of the `process()` method in NexisSignalEngine

        threat_report = detect_unicode_threat(input_signal)
        if threat_report["threat_level"] == "high":
            final_record = {
                "hash": self._hash(input_signal),
                "timestamp": datetime.utcnow().isoformat(),
                "input": input_signal,
                "threat_report": threat_report,
                "verdict": "blocked",
                "message": "Unicode-based threat detected. Input blocked."
            }
            self.cache[final_record["hash"]].append(final_record)
            self.memory[final_record["hash"]] = final_record
            self._save_memory()
            self._prune_and_rotate_memory()
            self.metrics.record_process_time(time.perf_counter() - start_time)
            logger.warning(f"Blocked Unicode threat: {input_signal}")
            return final_record
