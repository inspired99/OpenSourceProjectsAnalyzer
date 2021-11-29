package ru.hse.fcs.analyzer.service;

import io.micrometer.core.instrument.util.IOUtils;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

@Component
public class PythonService {

//    public static void main(String[] args) throws IOException, InterruptedException {
//        System.out.println(performAnalysis("https://github.com/angular/angular"));
//    }

    public String performAnalysis(String url) throws IOException, InterruptedException {
        ProcessBuilder processBuilder = new ProcessBuilder("python3", "src/main/resources/python/main.py");
        processBuilder.redirectErrorStream(true);

        Process process = processBuilder.start();
        OutputStream input = process.getOutputStream();
        input.write(url.getBytes(StandardCharsets.UTF_8));

        InputStream out = process.getInputStream();
        int exitCode = process.waitFor();
        return IOUtils.toString(out, StandardCharsets.UTF_8);
    }
}
