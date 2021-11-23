package ru.hse.fcs.analyzer.controllers;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import ru.hse.fcs.analyzer.model.Project;

import java.util.Collections;
import java.util.List;

@Controller
public class MainController {
    @Value("${welcome.message}")
    private String message;
    private final List<String> tasks = List.of("1", "2", "3", "4", "5");

    @GetMapping("/")
    public String main(Model model) {
        model.addAttribute("message", message);
        model.addAttribute("tasks", tasks);

        return "welcome";
    }

    @GetMapping("/hello")
    public String mainWithParam(@RequestParam(name="name", required = false, defaultValue = "") String name, Model model) {
        model.addAttribute("message", name);

        return "search";
    }

    @GetMapping("/search")
    @CrossOrigin(origins = "http://localhost:4200") //todo remove this
    public ResponseEntity<List<Project>> search(@RequestParam(name="url", required = false, defaultValue = "") String url) {
        Project project = new Project("https://github/vsplekhanov/OpenSourceProjectsAnalyzer", "OpenSourceProjectsAnalyzer", "Very good project");
        return ResponseEntity.ok(Collections.singletonList(project));
    }

}
